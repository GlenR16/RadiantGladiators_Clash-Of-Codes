const interestsInput = document.getElementById("interests");
const interestsList = document.getElementById("interestsList");
const profileForm = document.querySelector("form");

const domParser = new DOMParser();
interestsInput.addEventListener("change", addChip);
let interests = [];
Array.from(interestsList.children).forEach((chip)=>interests.push(chip.getAttribute("data_attr")))

function addChip(e){
    console.log(interestsList.children.length)
    const name = e.target.value || e;
    console.log(interests.includes(name))
    if(interests.includes(name) || interestsList.children.length>=5) return;
    interests.push(name);
    let chipTemplate = `
        <div data_attr="${name}" class="gap-x-3 mt-3 bg-neutral-700 inline p-2 rounded-3xl text-white">
            <input type="checkbox" hidden value="true" />
            <div class="inline">${name}</div>
            <span onclick="this.parentNode.remove()" >x</span> 
        </div>
    `
    let chip = domParser
        .parseFromString(chipTemplate, "text/html")
        .body.querySelector("div");
    interestsList.append(chip);
    document.getElementById("main_interests").value = interests;
}


function sendForm(){
    let interests = [];
    Array.from(interestsList.children).forEach((chip)=>interests.push(chip.getAttribute("data_attr")))
    document.getElementById("main_interests").value = interests;
    let formData = new FormData(profileForm);
    fetch("/profile/",{
        method: "POST",
        body: formData
    }).then((res)=>res.json())
    .then((data)=>{
    if (!data.submitted) return alert("Some Error occured!")
})
}