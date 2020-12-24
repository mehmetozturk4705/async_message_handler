## Asynchronous Message Handler

This package is a niche message handler solution between asyncio event loop and processes/threads (Aka multiprocessing.Process/threading.Thread).

You can install this package by 

    pip install async-message-handler
    

* AMH creates asynchronous connection between asyncio event loop and another python process/thread.

### How to use?

Code below shows basic usage of message handler api. This message api is completely nonblocking in asyncio event loop.

    import time
    import asyncio
    import multiprocessing as mp
    
    from asynchronous_message_handler import ProcessCommandHandler, CommandContext, ProcessCommand, Events
    
    #Creating new command handler object.
    handler = ProcessCommandHandler(timeout=15)
    
    def sample_process(context:CommandContext):
        #You should initialize context to be bound.
        context.initialize()
    
        #Waits until new message, this operation is blocking for this process.
        #If you want it to be nonblocking use blocking=False parameter.
    
        command:ProcessCommand = context.get_next()
        print(command.get_payload())
    
        #Sleep for 5 seconds.
        time.sleep(5)
        command.reply("Hello from process.")
    
        time.sleep(5)
        #Send message from process to asynchronous context.
        context.send_message("This is a late message from process.")
    
    
    #This is a sample event handler for new messages from process/thread.
    @handler.on(Events.NewMessage)
    def message_callback(message):
        print(message)
    
    
    async def main():
        #This is asyncio context.
        response = await handler.command("Hello from asyncio.")
        print(response)
        #Waiting for a while for sample process to loop message demo.
        await asyncio.sleep(8)
    
    
    
    if __name__=="__main__":
        process = mp.Process(target=sample_process, args=(handler.get_command_context(),))
        process.start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        process.join()
        
        
