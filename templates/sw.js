self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head ;
    const body = data.body;
    if (head && body){
         event.waitUntil(
            self.registration.showNotification(head, {
                body: body,
                icon: 'http://localhost:8000'+'/static/logo_.jpg'
            })
        );       
    }

    // Keep the service worker alive until the notification is created.

});