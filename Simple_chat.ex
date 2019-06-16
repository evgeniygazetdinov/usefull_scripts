#{:ok, pid} = Chat.Server.start_link remember
defmodule Simple_Chat do
    use GenServer
    def start_link do
        GenServer.start_link(__MODULE__,[])
    end
    def add_message(pid,message) do
        GenServer.cast(pid,{:add_message,message})
    end
    def get_messages(pid)do
        GenServer.call(pid,:get_messages)
    end

    def init(messages)do
        {:ok,messages}
    end
    def handle_cast({:add_message,new_message},messages) do
        {:noreply,[new_message|messages]}
    end
    def handle_call(:get_messages,_from,messages) do
        {:reply,messages,messages}
    end
end
