# control a vm on/off from the commandline

<hr>

[(see vmware KB link)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1038043)

### get a list of all VMs
`vim-cmd vmsvc/getallvms`

### power it up
`vim-cmd vmsvc/power.on ID_NUMBER`

### suspend it
`vim-cmd vmsvc/power.suspend ID_NUMBER`

### resume it
`vim-cmd vmsvc/power.suspend_resume ID_NUMBER`

### there are 'many' vmsvc commands you can run:

```
~ # vim-cmd vmsvc
Commands available under vmsvc/:
acquiremksticket                 get.snapshotinfo                 
acquireticket                    get.spaceNeededForConsolidation  
connect                          get.summary                      
convert.toTemplate               get.tasklist                     
convert.toVm                     getallvms                        
createdummyvm                    gethostconstraints               
destroy                          login                            
device.connection                logout                           
device.connusbdev                message                          
device.disconnusbdev             power.getstate                   
device.diskadd                   power.hibernate                  
device.diskaddexisting           power.off                        
device.diskremove                power.on                         
device.getdevices                power.reboot                     
device.toolsSyncSet              power.reset                      
device.vmiadd                    power.shutdown                   
device.vmiremove                 power.suspend                    
devices.createnic                power.suspendResume              
disconnect                       queryftcompat                    
get.capability                   reload                           
get.config                       setscreenres                     
get.config.cpuidmask             snapshot.create                  
get.configoption                 snapshot.dumpoption              
get.datastores                   snapshot.get                     
get.disabledmethods              snapshot.remove                  
get.environment                  snapshot.removeall               
get.filelayout                   snapshot.revert                  
get.filelayoutex                 snapshot.setoption               
get.guest                        tools.cancelinstall              
get.guestheartbeatStatus         tools.install                    
get.managedentitystatus          tools.upgrade                    
get.networks                     unregister                       
get.runtime                      upgrade                          
```

