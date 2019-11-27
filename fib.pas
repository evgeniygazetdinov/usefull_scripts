program fib_numbers;
var
    n, s: longint;





    function Fibonacci(n: integer): longint;
    var 
        i: integer;
        p, q, r: longint;
    begin
        if n <= 0 then 
            Fibonacci := 0
        else
        begin
            q := 0;
            r := 1;
            for i :=0 to n do 
            begin
                p := q;
                q := r;
                r := p + q
            end;
            Fibonacci := r
        end
    end;
begin
    readln(n);
    writeln(Fibonacci(n));
end.
