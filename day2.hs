{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Eta reduce" #-}
import Text.Parsec as P
import Text.Parsec.Token as PT
import Data.Char

number = many1 P.digit >>= \xs ->
    return $ foldl (\a b -> a*10 + Data.Char.ord b - 48) 0 xs

data Color = Green | Blue | Red

color = (do P.string "green"; return Green) <|>
    (do P.string "blue"; return Blue) <|>
    (do P.string "red"; return Red)

quantifiedColor = do
    n <- number
    P.spaces
    c <- color
    return (n, c)

incrRed n (r, g, b) = (r+n, g, b)
incrGreen n (r, g, b) = (r, g+n, b)
incrBlue n (r, g, b) = (r, g, b+n)

collate [] = (0, 0, 0) -- r, g b
collate ((n,c):xs) =
    (case c of
        Red -> incrRed
        Green -> incrGreen
        Blue -> incrBlue)
        n
    (collate xs)

draw = collate <$> sepBy1 quantifiedColor (do P.string ","; P.spaces)

game = sepBy1 draw (do P.string ";"; spaces)

labelledGame = do
    P.string "Game "
    gameNum <- number
    P.string ": "
    g <- game
    return (gameNum, g)

p = many1 (do g <- labelledGame; newline; return g)

possible (r, g, b) = r <= 12 && g <= 13 && b <= 14

possibleGames xs = [n | (n, ys) <- xs, all possible ys]

tuple1 (x, _, _) = x
tuple2 (_, x, _) = x
tuple3 (_, _, x) = x

minimumCubes xs = (
    maximum (map tuple1 xs),
    maximum (map tuple2 xs),
    maximum (map tuple3 xs)
  )

cubePower (r,g,b) = r*b*g

main1 = do
    contents <- readFile "day2.txt"
    let parsedFile = parse p "fuck you" contents
    case parsedFile of
        Left _ -> print parsedFile
        Right allGames ->
            print (sum (possibleGames allGames))

main2 = do
    contents <- readFile "day2.txt"
    let parsedFile = parse p "fuck you" contents
    case parsedFile of
        Left _ -> print parsedFile
        Right allGames ->
            let allGamesStripped = map snd allGames in
            print $
                sum $ map cubePower $ map minimumCubes allGamesStripped


-- Junk

ezparse p x = parse p "" x