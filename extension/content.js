function getPageContent() {
    const title = document.title || "";

    const headings = Array.from(
        document.querySelectorAll("h1, h2, h3, h4")
    )
        .map(element => element.innerText.trim())
        .filter(text => text.length > 0);

    const bodyText = document.body
        ? document.body.innerText
        : "";

    return {
        url: window.location.href,
        title: title,
        headings: headings,
        text: bodyText
    };
}

chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (message.action === "extractJob") {

            const data = getPageContent();

            sendResponse({
                success: true,
                data: data
            });
        }

        return true;
    }
);