document.getElementById("text1").addEventListener("keyup", testpassword2);
document.getElementById("text2").addEventListener("keyup", testpassword2);

function testpassword2() {
  var text1 = document.getElementById("text1");
  var text2 = document.getElementById("text2");
  if (text1.value == text2.value)
    label1.style.color = "#2EFE2E";
  else
    label1.style.color = "red";

}