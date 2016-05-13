﻿open System.Reflection
[<assembly: AssemblyTitle("Rts.Cms.WinService")>]
()

open System

open Topshelf
open Time

[<EntryPoint>]
let main argv =
  let info : string -> unit = fun s -> Console.WriteLine(sprintf "%s logger/Rts.Cms.WinService: %s" (DateTime.UtcNow.ToString("o")) s)
  let sleep (time : TimeSpan) = System.Threading.Thread.Sleep(time)

  let start hc =
    info "sample service starting"

    (s 30) |> HostControl.request_more_time hc
    sleep (s 1)

    Threading.ThreadPool.QueueUserWorkItem(fun cb ->
        sleep (s 3)
        info "requesting stop"
        hc |> HostControl.stop) |> ignore

    info "sample service started"
    true 
    
  let stop hc =
    info "sample service stopped"
    true
  
  Service.Default
  |> with_start start
  |> with_recovery (ServiceRecovery.Default |> restart (min 10))
  |> with_stop stop
  |> run
