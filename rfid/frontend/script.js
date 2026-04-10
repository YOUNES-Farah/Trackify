const SERVER_URL = "http://127.0.0.1:5000";

async function fetchAuthorizedUsers() {
    const response = await fetch(`${SERVER_URL}/authorized`);
    const data = await response.json();
    const tableBody = document.querySelector("#authorized-table tbody");
    tableBody.innerHTML = "";
    data.authorized_users.forEach(user => {
        const row = `<tr><td>${user.name}</td><td>${user.uid}</td></tr>`;
        tableBody.innerHTML += row;
    });
}

async function fetchAccessLogs() {
    const response = await fetch(`${SERVER_URL}/access_logs`);
    const data = await response.json();
    const tableBody = document.querySelector("#logs-table tbody");
    tableBody.innerHTML = "";
    data.access_logs.forEach(log => {
        const row = `<tr>
            <td>${log.name}</td>
            <td>${log.uid}</td>
            <td>${log.status}</td>
            <td>${log.timestamp}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

async function updateTables() {
    await fetchAuthorizedUsers();
    await fetchAccessLogs();
}

setInterval(updateTables, 5000);
updateTables();
