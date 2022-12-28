function theMostPowerfulWord(input) {
    let index = 0;
    let word = input[index];
    index++;
    let max = Number.MIN_SAFE_INTEGER;
    let powerWord = "";
 
 
    while (word !== "End of words") {
        let sum = 0;
 
        let symbol1 = word.charAt(0).toLowerCase();
        for (let i = 0; i < word.length; i++) {
            let symbol = Number(word.charCodeAt(i));
            sum += symbol;
 
        }
 
        if (symbol1 == "a" || symbol1 == "e" || symbol1 == "i" || symbol1 == "o" || symbol1 == "u" || symbol1 == "y") {
            sum *= word.length;
        } else {
            sum = Math.floor(sum / word.length);
        }
        if (max < sum) {
            max = sum;
            powerWord = word;
        }
 
        word = input[index];
        index++;
 
    }
 
    console.log(`The most powerful word is ${powerWord} - ${max}`);
 
}
