function openNav() {
    document.getElementById("mySidenav").style.width = "45%";
  }
  
function closeNav() {
document.getElementById("mySidenav").style.width = "0";
}
function showPopUp(){
	popup.style.display="block";
}
function hidePopUp(){
	popup.style.display="none";
}
function showStats(){
	stats.style.display="block";
}
function hideStats(){
	stats.style.display="none";
}
function night(){
	document.body.style.background = "linear-gradient(90deg, rgba(17,19,25,1) 0%, rgba(55,5,5,1) 50%, rgba(91,0,0,1) 100%)";
	nav.style.backgroundColor = "#bd5959";
	var elements = document.getElementsByClassName("article");
	for(var i = 0; i < elements.length; i++) {
		elements[i].style.backgroundColor = "#a22828";
	}
	
}
function day(){
	document.body.style.background = "linear-gradient(90deg, rgba(48,66,161,1) 0%, rgba(34,117,148,1) 50%, rgba(212,209,203,1) 100%)";
	nav.style.backgroundColor = "#eee";
	var elements = document.getElementsByClassName("article");
	for(var i = 0; i < elements.length; i++) {
		elements[i].style.backgroundColor = "#a6acf4";
	}
}