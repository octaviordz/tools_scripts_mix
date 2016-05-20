module Cmstool

open System
open System.IO
open System.Xml
open System.Xml.Linq
open System.Xml.XPath
open System.Text
open NLog
open NLog.Layouts
open System.IO

let machineConfigPath = "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\Config"
let websPath = "C:\\rts\\webs"
let log = LogManager.GetLogger "Cmstool"
let logConfig = NLog.Config.LoggingConfiguration()
let consoleTarget = new NLog.Targets.ColoredConsoleTarget()
logConfig.AddTarget("console", consoleTarget)
let fileTarget = new NLog.Targets.FileTarget()
logConfig.AddTarget("file", fileTarget)
//consoleTarget.Layout <- Layout.FromString @"${date:format=HH\:mm\:ss} ${logger} ${message}"
consoleTarget.Layout <- Layout.FromString @"${date:format=HH\:mm\:ss} ${message}"
fileTarget.FileName <- Layout.FromString "./logs/cmstool.${shortdate}.log"
let rule1 = new NLog.Config.LoggingRule("*", LogLevel.Trace, consoleTarget)
logConfig.LoggingRules.Add(rule1)
let rule2 = new NLog.Config.LoggingRule("Cmstool*", LogLevel.Trace, fileTarget)
logConfig.LoggingRules.Add(rule2)
LogManager.Configuration <- logConfig
let xn s = XName.Get(s)


let rec getAllFiles dir pattern =
    seq {
        yield! try Directory.EnumerateFiles(dir, pattern)
               with _ as ex -> Seq.empty<string>
        let dirs =
            try Directory.EnumerateDirectories(dir)
            with _ as ex -> Seq.empty<string>
        for d in dirs do
            yield! getAllFiles d pattern }


let analyzeWebConfig path defaultMap =
    sprintf "Analyzing %s" path |> log.Info
    let defaultMap = defaultArg defaultMap Map.empty
    let mutable result = defaultMap
    use reader = new StreamReader(path, Encoding.UTF8)
    let nav = XPathDocument(reader).CreateNavigator()
    let n = nav.SelectSingleNode(@"//configSections/section[@name='realcms']")
    let mutable isRtsCms = false
    if n <> null && n.MoveToAttribute("type", "") then
        if n.Value.Contains("Rts.Cms") then
            sprintf "Rts.Cms found at %s" (Path.GetDirectoryName path) |> log.Info
            isRtsCms <- true
    if not isRtsCms then
        result
    else
        let n = nav.SelectSingleNode(@"//system.web/pages")
        if n <> null && n.MoveToAttribute("validateRequest", "") then
            result <- Map.add @"//system.web/pages[validateRequest]" n.Value result
            if n.Value = "false"
            then sprintf "WARN: system.web/pages[validateRequest=\"false\"]" |> log.Info
        let n = nav.SelectSingleNode(@"//system.web/httpRuntime")
        if n <> null && n.MoveToAttribute("requestPathInvalidCharacters", "") then
            let v = n.Value
            let isValid (v : string) =
                if v = null then
                    true
                else
                    let required = "<,>,*,%,:,\\,?".Split [|','|] |> Set.ofArray
                    let input = v.Split([|','|], StringSplitOptions.RemoveEmptyEntries) |> Set.ofArray
                    Set.isSubset required input
            result <- Map.add @"//system.web/httpRuntime[requestPathInvalidCharacters]" v result
            if (isValid v) = false then
                sprintf "WARN: system.web/httpRuntime[requestPathInvalidCharacters] %A" v |> log.Info
        elif n <> null then
            result <- Map.add @"//system.web/httpRuntime[requestPathInvalidCharacters]" null result
            sprintf "WARN: system.web/httpRuntime[requestPathInvalidCharacters] %A" null |> log.Info
        if n <> null && n.MoveToAttribute("requestValidationMode", "") then
            result <- Map.add @"//system.web/httpRuntime[requestValidationMode]" n.Value result
            if n.Value = "2.0" then
                sprintf "WARN: system.web/httpRuntime[requestValidationMode] %A" n.Value |> log.Info
        result


let hasConfigIssue key value =
    match key with
    | @"//system.web/httpRuntime[requestPathInvalidCharacters]" ->
        let issue =
            match value with
            | "" -> true
            | null -> true
            | _ ->
                let required = "<,>,*,%,:,\\,?".Split [|','|] |> Set.ofArray
                let v =
                    value.Split([|','|], StringSplitOptions.RemoveEmptyEntries)
                    |> Set.ofArray
                not <| Set.isSubset required v
        issue, value
    | @"//system.web/pages[validateRequest]" ->
        (if value = "false" then true else false), value
    | _ -> false, String.Empty


let analyzeCmsSites searchPath machineConfigPath =
    let finding =
        getAllFiles machineConfigPath "web.config"
        |> Seq.map (fun fpath -> fpath, analyzeWebConfig fpath None)
        |> Seq.tryPick Some
    let mmap =
        match finding with
        | Some (_, map) -> Some(map)
        | None -> None
    getAllFiles searchPath "web.config"
    |> Seq.map (fun fpath -> fpath, (analyzeWebConfig fpath mmap))
    |> Seq.fold (fun filtered (path, map) ->
        let issues = map |> Map.filter (fun key value ->
            match hasConfigIssue key value with
            | true, _ -> true
            | _ -> false )
        if Map.isEmpty issues
        then filtered
        else Seq.append (seq[(path, issues)]) filtered
        ) Seq.empty


let updateWebConfig path =
    sprintf "Updating %s" path |> log.Info
    try
        let xdoc =
            use reader = new StreamReader(path, Encoding.UTF8)
            XDocument.Load(reader)
        let n = xdoc.XPathSelectElement(@"//system.web/httpRuntime")
        if n <> null then
            let attr = xn "requestPathInvalidCharacters" |> n.Attribute
            n.SetAttributeValue(xn "requestPathInvalidCharacters", "<,>,*,%,:,\\,?")
            let dir, fname, ext =
                Path.GetDirectoryName(path), Path.GetFileName(path), Path.GetExtension(path)
            let destfname = String.Join("", fname, "." + DateTime.Now.ToString("yyyy'-'MM'-'dd'T'HHmmss"), ext)
            let destFileName = Path.Combine([|dir; destfname|])
            File.Copy(path, destFileName, false)
            use writer = new StreamWriter(path, false, Encoding.UTF8)
            xdoc.Save(writer)
            true
        else
            false
    with _ as ex ->
        log.Error(ex, sprintf "Error updating %s" path)
        false


let updateWebConfigFiles files =
    files
    |> Seq.fold (fun filtered (path, issues) ->
        if updateWebConfig path = true
        then Seq.append (seq[(path, issues)]) filtered
        else filtered
        ) Seq.empty


let updateCmsSitesWebConfig searchPath =
    let mutable count = 0
    getAllFiles searchPath "web.config"
    |> Seq.iter (fun fpath ->
        if updateWebConfig fpath = true then
            count <- count + 1)
    sprintf "Finished with a total of %i file updated" count |> log.Info


[<EntryPoint>]
let main argv =
    //printfn "%A" argv
    let mutable cissues = 0
    let mutable cupdated = 0
    analyzeCmsSites websPath machineConfigPath
    |> Seq.iter (fun (path, issues) ->
        cissues <- cissues + 1
        sprintf "ISSUE: %s %A" path issues |> log.Warn
        if updateWebConfig path = true then
            cupdated <- cupdated + 1 )
    sprintf "Finished with a total of %i issues, %i web.config files upated" cissues cupdated |> log.Info
    0 // return an integer exit code
