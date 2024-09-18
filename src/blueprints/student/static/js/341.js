
// Fetch and update the student's phase when the page loads
window.addEventListener('load', updatePhase);

const PHASE_ONE_TEXT = 'Phase I - Green Card';
const PHASE_TWO_TEXT = 'Phase II - White Card';
const PHASE_THREE_TEXT = 'Phase III - Yellow Card';
const PHASE_FOUR_TEXT = 'Academic Study Program Phase - Blue Card';
const PHASE_FIVE_TEXT = 'Stalled Progression Phase/Phase-Base-(Red Card)';

var container = document.querySelector('.container');
var phaseInput;
/*Loading the phase change to the textbox on the window */
window.onload = async function() {
    
    phaseInput = document.getElementById('studentPhase');
    
    
    await updatePhase();
};

async function updatePhase() {
    try {
        const response = await fetch('/api/getStudentPhase'); // Replace with your actual API endpoint
        const data = await response.json();  

        phaseInput.value = data.phase; // Set the value of the text box
        
        // Apply color changes based on the phase
        applyColorChange(data.phase.toLowerCase());

    } catch (error) {
        console.error('Error fetching student phase:', error);
    }
}

function applyColorChange(phase) {
    phaseInput = document.getElementById('studentPhase');
    
    // Reset any previous classes
    phaseInput.className = '';

    // Apply new class based on the phase and phase color
    switch (phase) {
        case 'phase-1':
            phaseInput.classList.add('phase-1');
            phaseInput.value = PHASE_ONE_TEXT;
            container.style.backgroundColor = 'green';
            break;
        case 'phase-2':
            phaseInput.classList.add('phase-2');
            phaseInput.value = PHASE_TWO_TEXT;
            container.style.backgroundColor = 'white';
            break;
        case 'phase-3':
            phaseInput.classList.add('phase-3');
            phaseInput.value = PHASE_THREE_TEXT;
            container.style.backgroundColor = 'Yellow';
            break;
        case 'phase-4':
            phaseInput.classList.add('phase-4');
            phaseInput.value = PHASE_FOUR_TEXT;
            container.style.backgroundColor = 'blue';
            break;
        case 'phase-5':
            phaseInput.classList.add('phase-5');
            phaseInput.value = PHASE_FIVE_TEXT;
            container.style.backgroundColor = 'red';
            break;
    }
}

