const interestsInput = document.getElementById("interests");
const interestsList = document.getElementById("interestsList");
const domParser = new DOMParser();

interestsInput.addEventListener("change", addChip);

function addChip(e){
    const name = e.target.value;
    let chipTemplate = `
        <div class="gap-x-3 mt-3 bg-neutral-700 inline p-2 rounded-3xl text-white">
            <input type="checkbox" hidden name="${name}" value="true" />
            <div class="inline">${name}</div>
            <span onclick="this.parentNode.remove()" >x</span> 
        </div>
    `
    let chip = domParser
        .parseFromString(chipTemplate, "text/html")
        .body.querySelector("div");
    interestsList.append(chip)
}

