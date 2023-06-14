// The form we receive user input from
let chatForm = document.querySelector("#chatform");
let chatList = document.querySelector(".chatlist");
let currentWeight = 0;
let currentIntent = "";
let tempIntent = "";
let isReaction = false;

// The sender should be "user" or "bot"
function displayChatBubble(message, sender) {
    let chatBubble = document.createElement("li");
    chatBubble.classList.add(sender === "user" ? "user__input" : "bot__output");
    chatBubble.innerHTML = message;
    chatList.appendChild(chatBubble);
    //Sets chatList scroll to the bottom
    chatList.scrollTop = chatList.scrollHeight;
}

// function checkInput(input) {
//     if ((input == "có" || input.indexOf("có") >= 0) && tempIntent) {
//         for (let keyword in script) {
//             if (
//                 script[keyword].intent === tempIntent &&
//                 script[keyword].weight == 0
//             ) {
//                 currentWeight = script[keyword].weight;
//                 currentIntent = script[keyword].intent.slice();
//                 return script[keyword].responses;
//             }
//         }
//     }
//     if (input == "không" && tempIntent) {
//         return ["Okay ..."];
//     }
//     for (let keyword in script) {
//         if (input.indexOf(keyword) >= 0) {
//             if (
//                 script[keyword].intent != currentIntent &&
//                 script[keyword].weight != 0
//             ) {
//                 tempIntent = script[keyword].intent.slice();
//                 return [
//                     `Xin lỗi tôi không hiểu ngữ cảnh! Có phải bạn muốn hỏi về ${script[keyword].intent}?`,
//                 ];
//             } else {
//                 if (script[keyword].weight > currentWeight + 1) {
//                     return [`Xin cung cấp thêm thông tin về ${script[keyword].intent}!!`];
//                 }
//             }
//             currentWeight = script[keyword].weight;
//             currentIntent = script[keyword].intent.slice();
//             return script[keyword].responses;
//         }
//     }
//     return ["Xin lỗi tôi chưa hiểu ý bạn! Bạn có thể làm rõ hơn được không?"];
// }

const random = (min, max) => Math.floor(Math.random() * (max - min)) + min;

function makeResponse(input) {
    // let responseArr = checkInput(input);
    // if (responseArr) {
    //     return responseArr[random(0, responseArr.length)];
    // }
    // return "";
    return input;
}

function handleInput() {
    // The text area for user's input text
    let textInput = document.querySelector(".chatbox");
    let input = textInput.value.toLowerCase();
    //Check empty textarea
    if (input.length > 0) {
        displayChatBubble(input, "user");
        let response = makeResponse(input);
        if (response) {
            // if (Array.isArray(response)) {
            //     let animationCounter = 1;
            //     let animationBubbleDelay = 400;
            //     for (let i in response) {
            //         displayChatBubble(response[i], "bot");
            //         chatList.lastElementChild.style.animationDelay =
            //             animationCounter * animationBubbleDelay + "ms";
            //         animationCounter++;
            //         chatList.lastElementChild.style.animationPlayState = "running";
            //     }
            // } else {
            //     displayChatBubble(response, "bot");
            // }
            displayChatBubble(response, "bot");
        }
    }
    textInput.value = "";
}

window.onload = () => {
    // Handle Enter
    chatForm.addEventListener("keydown", (e) => {
        if (e.keyCode == 13) {
            e.preventDefault();
            handleInput();
        }
    });
    // Handle submit
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        handleInput();
    });
};