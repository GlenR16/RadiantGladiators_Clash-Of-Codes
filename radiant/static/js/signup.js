
function page2(){
    document.getElementById("page_1").classList.add("hidden");
    document.getElementById("page_2").classList.remove("hidden");
  }

  function page3(){
    document.getElementById("page_2").classList.add("hidden");
    document.getElementById("page_3").classList.remove("hidden");
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
    }).then((res)=>res.json)
    .then((data)=>{
      if(!data.submitted) return alert("Some error occured!")
      page2();
    })
  }