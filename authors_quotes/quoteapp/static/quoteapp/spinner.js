function showSpinner() {
        document.getElementById('spinner').style.display = 'block';
}

function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
}

function dismissAlert() {
        // Replace 'alertId' with the actual ID of your alert
        const alertElement = document.getElementById('alertId');

        if (alertElement) {
            const alert = new bootstrap.Alert(alertElement);
            alert.close();
        }
    }

function showAlert(message) {
    const alertContainer = document.getElementById('alertContainer');
    alertContainer.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert" id="alertId">
          <strong>${message}</strong>
          <button type="button" class="close" data-dismiss="alert" aria-label="Close" onclick="dismissAlert()">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
    `;
}

function makeAPICall() {
    let msg = 'Scraping has ended up successfully';
    let statusCode;
    showSpinner();

    fetch("/scrape")
        .then(response => {
            statusCode = response.status;
            if (statusCode >= 400) {
                return response.json().then(errorData => {
                    msg = `HTTP error! Status: ${statusCode}, Message: ${errorData.message}`;
                });
            }
        })
        .then(data => {
            // Process API response
            console.log(data);
        })
        .catch(error => msg = `Error: ${error.message}, status code: ${statusCode}`)
        .finally(() => {
            hideSpinner();
            console.log(msg);
            showAlert(msg);
        });
}
