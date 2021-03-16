function viewDiv(){
  var input = document.getElementById("popup");
  var opas = document.getElementById('op');   /*.style.visibility = "hidden";*/
  			
  if (input.getAttribute('class') == 'hidden') {
  	input.classList.remove('hidden');
  	opas.classList.add('visibility');
  } else {
  	 input.classList.add('hidden');
  	 opas.classList.remove('visibility');
  	}
};