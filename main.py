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