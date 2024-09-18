    
    
    // Add a new discrepancy entry
    function addDiscrepancy() {
        // Prompt user for input
        const date = prompt("Enter the date (YYYY-MM-DD):");
        const description = prompt("Enter the description:");
        
        if (date && description) {
            const statusOptions = `
                <select class="form-control">
                    <option value="resolved">Resolved</option>
                    <option value="unresolved">Unresolved</option>
                </select>
            `;
            const table = document.getElementById('discrepancyTable').getElementsByTagName('tbody')[0];
            const newRow = table.insertRow();
            newRow.innerHTML = `
                <td>${date}</td>
                <td>${description}</td>
                <td>${statusOptions}</td>
                <td><button class="btn btn-danger btn-sm" onclick="removeRow(this)">Remove</button></td>
            `;
        }
    }

    // Add a new excellence report entry
    function addExcellence() {
        const date = prompt("Enter the date (YYYY-MM-DD):");
        const description = prompt("Enter the description:");
        const award = prompt("Enter the award:");

        if (date && description && award) {
            const table = document.getElementById('excellenceTable').getElementsByTagName('tbody')[0];
            const newRow = table.insertRow();
            newRow.innerHTML = `
                <td>${date}</td>
                <td>${description}</td>
                <td>${award}</td>
                <td><button class="btn btn-danger btn-sm" onclick="removeRow(this)">Remove</button></td>
            `;
        }
    }

    // Remove a row from the table
    function removeRow(button) {
        const row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }