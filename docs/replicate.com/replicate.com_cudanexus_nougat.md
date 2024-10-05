Title: cudanexus/nougat – Replicate

URL Source: https://replicate.com/cudanexus/nougat

Markdown Content:
cudanexus/nougat – Run with an API on Replicate
===============

### [cudanexus](https://replicate.com/cudanexus) / nougat

Nougat: Neural Optical Understanding for Academic Documents

[Cold](https://replicate.com/docs/reference/how-does-replicate-work#cold-boots)

*   Public
*   211 runs
*   [GitHub](https://github.com/cudanexus/nougat)
*   [Paper](https://arxiv.org/abs/2308.13418)
*   [License](https://github.com/cudanexus/nougat)

[Run with an API](https://replicate.com/cudanexus/nougat/api)

[Playground](https://replicate.com/cudanexus/nougat) [API](https://replicate.com/cudanexus/nougat/api) [Examples](https://replicate.com/cudanexus/nougat/examples) [README](https://replicate.com/cudanexus/nougat/readme) [Versions](https://replicate.com/cudanexus/nougat/versions)

Input
-----

FormJSONNode.jsPythonHTTPCogDocker

pdf\_file

\*file

Upload a file from your machine

input the pdf

Run this model in Node.js with [one line of code](https://replicate.com/docs/get-started/nodejs#quickstart-scaffold-a-project-with-a-one-liner):

npx create-replicate --model=cudanexus/nougat

or set up a project from scratch

Install [Replicate’s Node.js client library](https://github.com/replicate/replicate-javascript)

```shell
npm install replicate
```

Copy

Set the `REPLICATE_API_TOKEN` environment variable

```shell
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

VisibilityCopy

Find your API token in [your account settings](https://replicate.com/account/api-tokens).

Import and set up the client

```javascript
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

Copy

Run cudanexus/nougat using Replicate’s API. Check out the [model's schema](https://replicate.com/cudanexus/nougat/api/schema) for an overview of inputs and outputs.

```javascript
const output = await replicate.run(
  "cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
  {
    input: {
      pdf_file: "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
    }
  }
);
console.log(output);
```

Copy

To learn more, take a look at [the guide on getting started with Node.js](https://replicate.com/docs/get-started/nodejs).

Install [Replicate’s Python client library](https://github.com/replicate/replicate-python)

```shell
pip install replicate
```

Copy

Set the `REPLICATE_API_TOKEN` environment variable

```shell
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

VisibilityCopy

Find your API token in [your account settings](https://replicate.com/account/api-tokens).

Import the client

```python
import replicate
```

Copy

Run cudanexus/nougat using Replicate’s API. Check out the [model's schema](https://replicate.com/cudanexus/nougat/api/schema) for an overview of inputs and outputs.

```python
output = replicate.run(
    "cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
    input={
        "pdf_file": "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
    }
)
print(output)
```

Copy

To learn more, take a look at [the guide on getting started with Python](https://replicate.com/docs/get-started/python).

Set the `REPLICATE_API_TOKEN` environment variable

```shell
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

VisibilityCopy

Find your API token in [your account settings](https://replicate.com/account/api-tokens).

Run cudanexus/nougat using Replicate’s API. Check out the [model's schema](https://replicate.com/cudanexus/nougat/api/schema) for an overview of inputs and outputs.

```shell
curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d $'{
    "version": "d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
    "input": {
      "pdf_file": "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
    }
  }' \
  https://api.replicate.com/v1/predictions
```

Copy

To learn more, take a look at [Replicate’s HTTP API reference docs](https://replicate.com/docs/reference/http).

Install [Cog](https://github.com/replicate/cog)

```shell
brew install cog
```

Copy

If you don’t have [Homebrew](https://brew.sh/), there are [other installation options available](https://github.com/replicate/cog#install).

Pull and run cudanexus/nougat using Cog (this will download the full model and run it in your local environment):

```shell
cog predict r8.im/cudanexus/nougat@sha256:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76 \
  -i 'pdf_file="https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"'
```

Copy

To learn more, take a look at [the Cog documentation](https://github.com/replicate/cog).

Pull and run cudanexus/nougat using Docker (this will download the full model and run it in your local environment):

```shell
docker run -d -p 5000:5000 --gpus=all r8.im/cudanexus/nougat@sha256:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76
```

Copy

Add a payment method to run this model.

[Each run costs approximately$0.08.](https://replicate.com/cudanexus/nougat#performance "See run time & cost for details") Alternatively, try out our [featured models](https://replicate.com/explore#featured-models) for free.

[Sign in with GitHub](https://replicate.com/login/github/?next=/cudanexus/nougat)By signing in, you agree to our  
[terms of service](https://replicate.com/terms) and [privacy policy](https://replicate.com/privacy)

Output
------

PreviewJSON

[tmpxzhzbfnicalculus00marciala\_0136\_formatted.txt](https://replicate.delivery/pbxt/1GebruSBYt14bCfN3Wz5zHAQb83V3R6ct62TEefzHkSLogjIB/tmpxzhzbfnicalculus00marciala_0136_formatted.txt)

```
{
  "completed_at": "2024-01-03T21:24:18.945347Z",
  "created_at": "2024-01-03T21:17:48.622997Z",
  "data_removed": false,
  "error": null,
  "id": "p3jvmurbfvunl62p5c2zf5tvyy",
  "input": {
    "pdf_file": "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
  },
  "logs": "file_name is - /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf\nrunning---------subprocess\nCompletedProcess(args=['nougat', '--out', 'output', 'pdf', '/tmp/tmpxzhzbfnicalculus00marciala_0136.pdf', '--checkpoint', 'nougat', '--markdown', '--no-skipping'], returncode=0, stdout='', stderr='/root/.pyenv/versions/3.8.18/lib/python3.8/site-packages/torch/functional.py:504: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at ../aten/src/ATen/native/TensorShape.cpp:3526.)\\n  return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]\\n\\n  0%|          | 0/1 [00:00<?, ?it/s]INFO:root:Processing file /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf with 1 pages\\n\\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\\n-> Cannot close object, library is destroyed. This may cause a memory leak!\\n')\n----------------- /src\n/src/output/tmpxzhzbfnicalculus00marciala_0136_formatted.txt",
  "metrics": {
    "predict_time": 18.405277,
    "total_time": 390.32235
  },
  "output": "https://replicate.delivery/pbxt/1GebruSBYt14bCfN3Wz5zHAQb83V3R6ct62TEefzHkSLogjIB/tmpxzhzbfnicalculus00marciala_0136_formatted.txt",
  "started_at": "2024-01-03T21:24:00.540070Z",
  "status": "succeeded",
  "urls": {
    "get": "https://api.replicate.com/v1/predictions/p3jvmurbfvunl62p5c2zf5tvyy",
    "cancel": "https://api.replicate.com/v1/predictions/p3jvmurbfvunl62p5c2zf5tvyy/cancel"
  },
  "version": "d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76"
}
```

Copy

Generated in

18.4 seconds

[Tweak it](https://replicate.com/cudanexus/nougat/versions/d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76?prediction=p3jvmurbfvunl62p5c2zf5tvyy)Download[Report](https://replicate.com/p/p3jvmurbfvunl62p5c2zf5tvyy/report)

Show logs

```
file_name is - /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf
running---------subprocess
CompletedProcess(args=['nougat', '--out', 'output', 'pdf', '/tmp/tmpxzhzbfnicalculus00marciala_0136.pdf', '--checkpoint', 'nougat', '--markdown', '--no-skipping'], returncode=0, stdout='', stderr='/root/.pyenv/versions/3.8.18/lib/python3.8/site-packages/torch/functional.py:504: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at ../aten/src/ATen/native/TensorShape.cpp:3526.)\n  return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]\n\n  0%|          | 0/1 [00:00<?, ?it/s]INFO:root:Processing file /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf with 1 pages\n\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\n-> Cannot close object, library is destroyed. This may cause a memory leak!\n')
----------------- /src
/src/output/tmpxzhzbfnicalculus00marciala_0136_formatted.txt
```

Copy logsFullscreen logsDownload logs

#### Run time and cost

This model costs approximately $0.081 to run on Replicate, or 12 runs per $1, but this varies depending on your inputs. It is also open source and you can [run it on your own computer with Docker](https://replicate.com/cudanexus/nougat/api).

This model runs on [Nvidia T4 GPU hardware](https://replicate.com/docs/billing). Predictions typically complete within 7 minutes. The predict time for this model varies significantly based on the inputs.

#### Readme

Nougat OCR
==========

Introduction
------------

This repository contains the source code for Nougat OCR, a tool for Optical Character Recognition (OCR) using the Nougat model. Follow the instructions below to set up the environment and run the OCR.

Installation
------------

1.  Clone this repository: \`\`\`bash

git clone [https://github.com/cudanexus/nougat.git](https://github.com/cudanexus/nougat.git) \`\`\`

1.  Download the model files from Hugging Face using Git LFS:
2.  Make sure you have Git LFS installed (Git LFS Installation )
3.  Run the following commands:

```bash
git lfs install
git clone https://huggingface.co/spaces/tomriddle/nougat
```

Copy

2\. After the above commands, your folder structure should look like this:
--------------------------------------------------------------------------

```lua
input
Upload nougat.pdf
nougat
output
Upload nougat.pdf
README.md
app.py
requirements.txt
```

Copy

3\. Copy the `nougat` folder (which contains all model files) to the root of this repository. Your updated structure should look like:
--------------------------------------------------------------------------------------------------------------------------------------

```lua
input
nougat
--- config.json
--- pytorch_model.bin
--- special_tokens_map.json
--- tokenizer.json
--- tokenizer_config.json
output
app.py
cog.yaml
output.txt
predict.py
requirements.txt
```

Copy

4\. Install the required Python packages:
-----------------------------------------

```bash
pip install -r requirements.txt
```

Copy

Testing
-------

Ensure that everything is installed correctly by running:

```bash
python app.py --pdf_file input/nougat.pdf
```

Copy

If the installation is successful, you should see the OCR output.

Additional Information
----------------------

For any issues or questions, please refer to the [repository](https://github.com/cudanexus/nougat) or contact the repository owner.

[Replicate](https://replicate.com/)

**This model is cold.** You'll get a fast response if the model is warm and already running, and a slower response if the model is cold and starting up.

Choose a file from your machine

Hint: you can also drag files onto the input

Logs (p3jvmurbfvunl62p5c2zf5tvyy)
=================================

Succeeded

```
file_name is - /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf
running---------subprocess
CompletedProcess(args=['nougat', '--out', 'output', 'pdf', '/tmp/tmpxzhzbfnicalculus00marciala_0136.pdf', '--checkpoint', 'nougat', '--markdown', '--no-skipping'], returncode=0, stdout='', stderr='/root/.pyenv/versions/3.8.18/lib/python3.8/site-packages/torch/functional.py:504: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at ../aten/src/ATen/native/TensorShape.cpp:3526.)\n  return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]\n\n  0%|          | 0/1 [00:00<?, ?it/s]INFO:root:Processing file /tmp/tmpxzhzbfnicalculus00marciala_0136.pdf with 1 pages\n\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\n100%|██████████| 1/1 [00:06<00:00,  6.30s/it]\n-> Cannot close object, library is destroyed. This may cause a memory leak!\n')
----------------- /src
/src/output/tmpxzhzbfnicalculus00marciala_0136_formatted.txt
```

