{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Eta reduce" #-}
import Data.List
import Text.Parsec as P
import Text.Parsec.Token as PT
import Data.Char

-- Card   1: 81  1 43 40 49 51 38 65 36  4 | 21 15  1 43 60  9 83 81 35 49 40 38 82 65 20  4 58 94 16 89 84 10 77 48 76

number = many1 P.digit >>= \xs ->
    return $ foldl (\a b -> a*10 + Data.Char.ord b - 48) 0 xs

ident = do P.string "Card"; spaces; result <- number; P.string ":"; spaces; return result

line = do
    i <- ident ; 
    winning <- many1 (do x <- number; spaces; return x)
    P.string "|"
    spaces
    have <- many1 (do x <- number; spaces; return x)
    let matches = winning `intersect` have
    return (length matches)


parseIn = do
    contents <- readFile "day4.txt"
    let parsedFile = parse (many1 line) "fuck you" contents
    return parsedFile

crazyCopy [] = []
crazyCopy (0:xs) = crazyCopy xs
crazyCopy (x:xs) = [x] ++ concatMap crazyCopy (take x (tails xs)) ++ crazyCopy xs

notSoCrazyCopy [] = [0]
notSoCrazyCopy (x:xs) = [x + sum (take x (notSoCrazyCopy xs))] ++ notSoCrazyCopy xs

main = do
    Right xs <- parseIn
    print (sum $ notSoCrazyCopy xs)