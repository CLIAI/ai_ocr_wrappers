Title: cudanexus/nougat – Replicate

URL Source: https://replicate.com/cudanexus/nougat/api

Markdown Content:
cudanexus/nougat – API reference
===============

[](https://replicate.com/ "Replicate")
======================================

[Explore](https://replicate.com/explore) [Pricing](https://replicate.com/pricing) [Docs](https://replicate.com/docs) [Blog](https://replicate.com/blog) [Changelog](https://replicate.com/changelog) [Sign in](https://replicate.com/signin?next=/cudanexus/nougat/api) [Get started](https://replicate.com/docs)

Menu

[Explore](https://replicate.com/explore)[Pricing](https://replicate.com/pricing)[Docs](https://replicate.com/docs)[Blog](https://replicate.com/blog)[Changelog](https://replicate.com/changelog)[Sign in](https://replicate.com/signin)

![Image 1](https://github.com/cudanexus.png)

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

Run cudanexus/nougat with an API

Table of Contents

[Get started](https://replicate.com/cudanexus/nougat/api)

[Learn more](https://replicate.com/cudanexus/nougat/api/learn-more)

[Schema](https://replicate.com/cudanexus/nougat/api/schema)

[API reference](https://replicate.com/cudanexus/nougat/api/api-reference)

Use one of our client libraries to get started quickly.

Node.js

Python

HTTP

Set the `REPLICATE_API_TOKEN` environment variable

```shell
export REPLICATE_API_TOKEN=<paste-your-token-here>
```

VisibilityCopy

[Learn more about authentication](https://replicate.com/cudanexus/nougat/api/learn-more#authentication)Install Replicate’s Node.js client library

```shell
npm install replicate
```

Copy

[Learn more about setup](https://replicate.com/cudanexus/nougat/api/learn-more#setup)Run **cudanexus/nougat** using Replicate’s API. Check out the model's [schema](https://replicate.com/cudanexus/nougat/api/schema) for an overview of inputs and outputs.

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

Copy

[Learn more](https://replicate.com/cudanexus/nougat/api/learn-more)

[Replicate](https://replicate.com/)

[Home](https://replicate.com/home) [About](https://replicate.com/about) [Guides](https://replicate.com/guides) [Newsletter](https://replicate.com/newsletter) [Terms](https://replicate.com/terms) [Privacy](https://replicate.com/privacy) [Status](https://replicatestatus.com/) [GitHub](https://github.com/replicate) [X](https://x.com/replicate) [Discord](https://discord.gg/replicate) [Support](https://replicate.com/support) 

  

Copy model name

**This model is cold.** You'll get a fast response if the model is warm and already running, and a slower response if the model is cold and starting up.

System theme

Light theme

Dark theme

Show

Copy

Copy

Copy
