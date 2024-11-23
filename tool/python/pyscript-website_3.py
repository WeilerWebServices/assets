<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

 

    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />

    <script defer src="https://pyscript.net/alpha/pyscript.js"></script>

 

    <title>PyScript Demo</title>

</head>

<body>

    <py-script>

        name = "GeeksforGeeks"

        freq = {}

        for s in name:

            key = freq.keys()

            if s in key:

                freq[s] += 1

            else:

                freq[s] = 1

 

        for k in freq:

            print(f"{k} : {freq[k]}")

    </py-script>

</body>

</html>