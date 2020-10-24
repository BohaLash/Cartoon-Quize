var eyes = document.getElementsByClassName("eyes");
document.onmousemove = function(){
	var x = event.clientX * 100 / window.innerWidth + "%";
	var y = event.clientY * 100 / window.innerHeight + "%";
    eyes[0].style.left = x;
    eyes[0].style.top = y;
    eyes[0].style.transform = "translate(-"+x+",-"+y+")";
}