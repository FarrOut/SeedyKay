
exports.handler = async function(event) {
    console.log("request:", JSON.stringify(event, null, 2));
    return {
        statusCode: 200,
        headers: { "Content-Type": "text/plain" },
        body: `Hello, AWS Solutions Constructs! You've hit ${event.path}\n`
    };
};
