defmodule Counter do
    def countdown(from) when from >0  do
       :timer.sleep(1000)
       IO.inspect(from)
        countdown(from-1)
        
    end
    def countdown do
        IO.puts("blastoff")
    end
end
