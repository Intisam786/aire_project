function approveIncident(id) {
    fetch('/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ incident_id: id })
    }).then(() => location.reload());
}
function rejectIncident(id) {
    fetch('/reject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ incident_id: id })
    }).then(() => location.reload());
}
