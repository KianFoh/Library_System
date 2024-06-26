function updateUsernameFields() {
    const numberOfUsers = parseInt(document.getElementById('id_number_of_users').value);
    const usernamesContainer = document.getElementById('usernames-container');
    const currentUsername = document.getElementById('current-username').value;
    usernamesContainer.innerHTML = ''; // Clear any existing content

    for (let i = 1; i <= numberOfUsers; i++) {
        const label = document.createElement('label');
        label.textContent = `Username ${i}: `;
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `username_${i}`;
        input.id = `id_username_${i}`;
        input.maxLength = 100;
        input.className = 'form-control';  // Apply Bootstrap styling
        input.required = true;

        if (i === 1 && currentUsername) {
            input.value = currentUsername; // Set the first field to the current user's username
            input.readOnly = true;
        }

        if(!currentUsername){
            input.readOnly = true;
        }

        usernamesContainer.appendChild(label);
        usernamesContainer.appendChild(input);
        usernamesContainer.appendChild(document.createElement('br'));
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateUsernameFields(); // Update fields on initial load based on initial number of users
    document.getElementById('id_number_of_users').addEventListener('change', updateUsernameFields);
});
