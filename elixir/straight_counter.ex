defmodule Straight do
    def counter(limiter)do
        counter(1,limiter)
    end
    defp counter(count,limiter) when count <= limiter do
        IO.puts(count)
        counter(count+1,limiter)
        #undestand later why he put -
        IO.puts("this c #{count}")
        IO.puts(limiter)
    end
    defp counter(_counter,_limiter) do
        IO.puts("finish him")
    end
end
