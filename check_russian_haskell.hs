{-# LANGUAGE OverloadedStrings #-}
module Main where

import System.IO

main :: IO ()
main = do
    hSetBuffering stdout NoBuffering
    putStrLn "=== Data.Text test ==="
    putStrLn "Как вас зовут?"
    name <- getLine
    putStrLn $ concat ["Привет ",name,"!"]
    putStrLn "=== String test ==="
    putStrLn "А вас как зовут?"
    name <- getLine
    putStrLn $ concat ["Привет ",name,"!"]                                             
