## Asynchronous Message Handler

This package is a niche message handler solution between asyncio event loop and processes/threads (Aka multiprocessing.Process/threading.Thread).

You can install this package by 

    pip install asynchronous-message-handler
    

* AMH creates asynchronous connection between asyncio event loop and another python process/thread.

* For now, AMH only supports sending commands or primitive payloads from asyncio event loop to Process/Thread, and Process can respond incoming ProcessCommand object.


### How to use?

Code below shows basic usage of message handler api. This message api is completely nonblocking in asyncio event loop.

    import time
    import asyncio
    import multiprocessing as mp
    
    from asynchronous_message_handler import ProcessCommandHandler, CommandContext, ProcessCommand
    
    #Creating new command handler object.
    handler = ProcessCommandHandler(timeout=15)
    
    def sample_process(context:CommandContext):
        #You should initialize context to listen for messages.
        context.initialize()

        #Waits until new message, this operation is blocking for this process.
        #If you want it to be nonblocking use blocking=False parameter.
    
        command:ProcessCommand = context.get_next()
        print(command.get_payload())
    
        #Sleep for 5 seconds.
        time.sleep(5)
        command.reply("Hello from process.")


    async def main():
        #This is asyncio context.
        response = await handler.command("Hello from asyncio.")
        print(response)
    
    
    if __name__=="__main__":
        process = mp.Process(target=sample_process, args=(handler.get_command_context(),))
        process.start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        process.join()


    
 

