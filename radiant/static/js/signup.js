
function page2(){
    console.log(document.getElementById("first_page"));
    document.getElementById("first_page").classList.add("hidden");
    console.log(document.getElementById("second_page"));
    document.getElementById("second_page").classList.remove("hidden");
  }

  function page3(){
    document.getElementById("second_page").classList.add("hidden");
    document.getElementById("third_page").classList.remove("hidden");
  }

function get_otp(){
    const csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    const fileInput = document.getElementById("file-upload");
    const firstName = document.getElementById("first-name");
    const dateOfBirth = document.getElementById("dob");
    const gender = document.querySelector("input[name='gender']:checked")
    const email = document.getElementById("email-address");
    const phone = document.getElementById("phone");
    const toDate = document.querySelector( 'input[name="to-date"]:checked')
    const password1 = document.getElementById("password");
    const password2 = document.getElementById("c_password");
        if(
            !(firstName.value &&
            phone.value &&
            email.value &&
            dateOfBirth.value &&
            gender.value &&
            fileInput.files[0] &&
            toDate &&
            password1 &&
            password2)
        )
            return alert("Some fields are missing!")
        let formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrfTokenInput.value);
        formData.append("name", firstName.value);
        formData.append("phone", phone.value);
        formData.append("email", email.value);
        formData.append("dob", dateOfBirth.value);
        formData.append("gender", gender.value);
        formData.append("verification_file", fileInput.files[0]);
        formData.append("who_to_date", toDate);
        formData.append("password1", password1);
        formData.append("password2", password2);
        fetch("/get_otp/", {
        method:"POST",
        body: formData
        }).then((res)=>res.json())
        .then((data)=>{
        document.getElementById("uid").value = data.id;
        document.getElementById("c_otp").classList.remove("hidden");
        document.getElementById("send_otp_button").innerText = "Check OTP";
        document.getElementById("send_otp_button").onclick = check_otp;
    })
}

function check_otp(){
    const csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    const id = document.getElementById("uid");
    const otp = document.getElementById("otp");
    if(!(id.value &&otp.value ))
        return alert("Some fields are missing!");
    let formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfTokenInput.value);
    formData.append("id", id.value);
    formData.append("otp", otp.value);
    fetch("/check_otp/", {
        method:"POST",
        body: formData
        }).then((res)=>res.json())
        .then((data)=>{
        if(!data.correct) return alert("Incorrect OTP!")
        document.getElementById("c_otp").setAttribute("readonly",true);
        document.getElementById("nextbutton").removeAttribute("disabled");
    })
}