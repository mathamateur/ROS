function viewDiv() {
  var input = document.getElementById("popup");
  var opas = document.getElementById('op');
			
  input.classList.remove('hidden');
  opas.classList.add('visibility');
};

function hidDiv() {
  input.classList.add('hidden');
  opas.classList.remove('visibility');
}