# cudanexus/nougat – API Reference

## Authentication

Set the `REPLICATE_API_TOKEN` environment variable:

```shell
export REPLICATE_API_TOKEN=r8_6bj**********************************
```

[Learn more about authentication](https://replicate.com/cudanexus/nougat/api/learn-more#authentication)

## API Usage

Run **cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76** using Replicate's API. Check out the model's [schema](https://replicate.com/cudanexus/nougat/api/schema) for an overview of inputs and outputs.

### Bash

```bash
curl --silent --show-error https://api.replicate.com/v1/predictions \
    --request POST \
    --header "Authorization: Bearer $REPLICATE_API_TOKEN" \
    --header "Content-Type: application/json" \
    --header "Prefer: wait" \
    --data @- <<-EOM
{
    "version": "d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
    "input": {
        "pdf_file": "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
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
    "pdf_file": "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
}

output = replicate.run(
    "cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
    input=input
)
print(output)
#=> "https://replicate.delivery/pbxt/1GebruSBYt14bCfN3Wz5zHAQ...
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
    pdf_file: "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
};

const output = await replicate.run("cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76", { input });
console.log(output)
//=> "https://replicate.delivery/pbxt/1GebruSBYt14bCfN3Wz5zHAQ...
```

## Additional Information

- [Learn more about setup](https://replicate.com/cudanexus/nougat/api/learn-more#setup)
- [Model schema](https://replicate.com/cudanexus/nougat/api/schema)

