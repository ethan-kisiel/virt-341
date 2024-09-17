

function updatePhase() {
   
    const selectedPhase = document.getElementById('phaseSelect').value;  // Get the selected phase from dropdown
    const container = document.getElementById('phaseContainer'); // Get the container element
    
    container.className = 'container'; // Reset to default 
    container.classList.add(selectedPhase); // Add the selected phase
    document.getElementById('phaseName').textContent = selectedPhase.replace('-', ' ').toUpperCase();  //show the selected phase
}