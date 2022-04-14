// let myHeading = document.querySelector('title');
// myHeading.textContent = 'Hello world!';
// document.querySelector('html').onclick = function() {
//     alert('别戳我，我怕疼。');
// }
let myButton = document.querySelector('button');
let myHeading = document.querySelector('title');
function setUserName() {
  let myName = prompt('请输入你的名字。');
  if(!myName) {
    setUserName();
  } else {
    localStorage.setItem('name', myName);
    myHeading.innerHTML = 'Mozilla 酷毙了，' + myName;
  }
}
if(!localStorage.getItem('name')) {
  setUserName();
} else {
  let storedName = localStorage.getItem('name');
  myHeading.textContent = 'Mozilla 酷毙了，' + storedName;
}
myButton.onclick = function() {
   setUserName();
}

