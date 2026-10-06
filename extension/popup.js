document
    .getElementById("analyzeButton")
    .addEventListener("click", async () => {

        const status =
            document.getElementById("status");

        status.innerText =
            "Reading job page...";

        try {

            const tabs = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            const tab = tabs[0];

            chrome.tabs.sendMessage(
                tab.id,
                {
                    action: "extractJob"
                },
                (response) => {

                    if (chrome.runtime.lastError) {

                        status.innerText =
                            "Unable to read this webpage.";

                        return;
                    }

                    if (!response || !response.success) {

                        status.innerText =
                            "Could not extract job information.";

                        return;
                    }

                    console.log(response.data);

                    status.innerText =
                        "Job information extracted successfully.";

                    console.log(
                        "URL:",
                        response.data.url
                    );

                    console.log(
                        "Title:",
                        response.data.title
                    );

                    console.log(
                        "Text:",
                        response.data.text
                    );
                }
            );

        } catch (error) {

            console.error(error);

            status.innerText =
                "An error occurred.";
        }
    });