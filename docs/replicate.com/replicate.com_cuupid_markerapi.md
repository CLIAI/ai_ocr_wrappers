# cuuupid/marker – API Reference

## Authentication

Set the `REPLICATE_API_TOKEN` environment variable:

```shell
export REPLICATE_API_TOKEN=r8_6bj**********************************
```

[Learn more about authentication](https://replicate.com/cuuupid/marker/api/learn-more#authentication)

## API Usage

Run **cuuupid/marker:9c67051309f6d10ca139489f15fcb5ebc4866a3734af537c181fb13bc719d280** using Replicate's API. Check out the model's [schema](https://replicate.com/cuuupid/marker/api/schema) for an overview of inputs and outputs.

### HTTP

```bash
curl --silent --show-error https://api.replicate.com/v1/predictions \
    --request POST \
    --header "Authorization: Bearer $REPLICATE_API_TOKEN" \
    --header "Content-Type: application/json" \
    --header "Prefer: wait" \
    --data @- <<-EOM
{
    "version": "9c67051309f6d10ca139489f15fcb5ebc4866a3734af537c181fb13bc719d280",
    "input": {
        "document": "https://replicate.delivery/pbxt/K0onIKM1Wn5xTzan7ua67mqePVrRf6feas4sfTjbbAROkrcL/The%20Tell-Tale%20Heart.pdf",
        "parallel_factor": 10
    }
}
EOM
```

### Python

1. Install Replicate's Python client library:

```shell
pip install replicate
```

2. Use the API:

```python
import replicate

input = {
    "document": "https://replicate.delivery/pbxt/K0onIKM1Wn5xTzan7ua67mqePVrRf6feas4sfTjbbAROkrcL/The%20Tell-Tale%20Heart.pdf",
    "parallel_factor": 10
}

output = replicate.run(
    "cuuupid/marker:9c67051309f6d10ca139489f15fcb5ebc4866a3734af537c181fb13bc719d280",
    input=input
)
print(output)
#=> {"markdown":"https://replicate.delivery/pbxt/8UKRTTBKhe3u...
```

### Node.js

1. Install Replicate's Node.js client library:

```shell
npm install replicate
```

2. Use the API:

```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const input = {
    document: "https://replicate.delivery/pbxt/K0onIKM1Wn5xTzan7ua67mqePVrRf6feas4sfTjbbAROkrcL/The%20Tell-Tale%20Heart.pdf",
    parallel_factor: 10
};

const output = await replicate.run("cuuupid/marker:9c67051309f6d10ca139489f15fcb5ebc4866a3734af537c181fb13bc719d280", { input });
console.log(output)
//=> {"markdown":"https://replicate.delivery/pbxt/8UKRTTBKhe3u...
```

[Learn more about setup](https://replicate.com/cuuupid/marker/api/learn-more#setup)
```

This Markdown file organizes the API reference for cuuupid/marker, including:

1. A title and brief introduction
2. Authentication instructions
3. API usage examples for HTTP, Python, and Node.js
4. Installation instructions for the client libraries
5. Links to additional resources and documentation

The content is structured using proper Markdown syntax, including headings, code blocks, and links.

