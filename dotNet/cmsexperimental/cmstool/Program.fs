module Cmstool

open System
open System.IO
open System.Xml
open System.Xml.Linq
open System.Xml.XPath
open System.Text
open NLog
open NLog.Layouts

let machineConfigPath = "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\Config"
let websPath = "C:\\rts\\webs"
let log = LogManager.GetLogger "Cmstool"
let logConfig = NLog.Config.LoggingConfiguration()
let consoleTarget = new NLog.Targets.ColoredConsoleTarget()
logConfig.AddTarget("console", consoleTarget)
let fileTarget = new NLog.Targets.FileTarget();
logConfig.AddTarget("file", fileTarget)
//consoleTarget.Layout <- Layout.FromString @"${date:format=HH\:mm\:ss} ${logger} ${message}"
consoleTarget.Layout <- Layout.FromString @"${date:format=HH\:mm\:ss} ${message}"
fileTarget.FileName <- Layout.FromString "./logs/cmstool.${shortdate}.log"
let rule1 = new NLog.Config.LoggingRule("*", LogLevel.Trace, consoleTarget);
logConfig.LoggingRules.Add(rule1);
let rule2 = new NLog.Config.LoggingRule("Cmstool*", LogLevel.Trace, fileTarget);
logConfig.LoggingRules.Add(rule2);
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


let analyzeWebConfig (path : string) defaultMap =
    sprintf "Analyzing %s" path |> log.Info
    let defaultMap = defaultArg defaultMap Map.empty
    let mutable result = defaultMap
    use reader = new StreamReader(path, Encoding.UTF8)
    let nav = XPathDocument(reader).CreateNavigator()
    let n = nav.SelectSingleNode(@"//system.web/pages")
    if n <> null && n.MoveToAttribute("validateRequest", "") then
        result <- Map.add @"//system.web/pages[validateRequest]" n.Value result
        if n.Value = "false"
        then sprintf "WARN: system.web/pages[validateRequest=\"false\"]" |> log.Info
    let n = nav.SelectSingleNode(@"//system.web/httpRuntime")
    if n <> null && n.MoveToAttribute("requestPathInvalidCharacters", "") then
        let v = n.Value
        result <- Map.add @"//system.web/httpRuntime[requestPathInvalidCharacters]" v result
        if v <> null then
            sprintf "WARN: system.web/httpRuntime[requestPathInvalidCharacters] %A" v |> log.Info
    if n <> null && n.MoveToAttribute("requestValidationMode", "") then
        result <- Map.add @"//system.web/httpRuntime[requestValidationMode]" n.Value result
        if n.Value = "2.0" then
            sprintf "WARN: system.web/httpRuntime[requestValidationMode] %A" n.Value |> log.Info
    result


let hasConfigIssue key value =
    match key with
    | @"//system.web/httpRuntime[requestPathInvalidCharacters]" ->
        let issue = if value = String.Empty then true else false
        issue, value
    | @"//system.web/pages[validateRequest]" ->
        (if value = "false" then true else false), value
    | _ -> false, String.Empty


let analyzeCmsSites =
    let finding =
        getAllFiles machineConfigPath "web.config"
        |> Seq.map (fun fpath -> fpath, analyzeWebConfig fpath None)
        |> Seq.tryPick Some
    let mmap =
        match finding with
        | Some (_, map) -> Some(map)
        | None -> None
    let mutable cissues = 0
    getAllFiles websPath "web.config"
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
    |> Seq.iter (fun (path, issues) -> 
        cissues <- cissues + 1
        sprintf "ISSUE: %s %A" path issues |> log.Warn)
    sprintf "Finished with a total of %i issues" cissues |> log.Info


[<EntryPoint>]
let main argv = 
    //printfn "%A" argv
    analyzeCmsSites
    0 // return an integer exit code
