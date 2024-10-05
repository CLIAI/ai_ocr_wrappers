Title: cudanexus/nougat – Replicate

URL Source: https://replicate.com/cudanexus/nougat/api/api-reference

Markdown Content:
cudanexus/nougat – API reference
===============

[](https://replicate.com/ "Replicate")
======================================

[Explore](https://replicate.com/explore) [Pricing](https://replicate.com/pricing) [Docs](https://replicate.com/docs) [Blog](https://replicate.com/blog) [Changelog](https://replicate.com/changelog) [Sign in](https://replicate.com/signin?next=/cudanexus/nougat/api/api-reference) [Get started](https://replicate.com/docs)

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

Create a prediction

predictions.create

Request body

*   inputobjectRequired
    
    The model's input as a JSON object. The input schema depends on what model you are running. To see the available inputs, click the "API" tab on the model you are running or [get the model version](https://replicate.com/cudanexus/nougat/api/api-reference#models.versions.get) and look at its `openapi_schema` property. For example, [stability-ai/sdxl](https://replicate.com/stability-ai/sdxl) takes `prompt` as an input.
    
    Files should be passed as HTTP URLs or data URLs.
    
    Use an HTTP URL when:
    
    *   you have a large file \> 256kb
    *   you want to be able to use the file multiple times
    *   you want your prediction metadata to be associable with your input files
    
    Use a data URL when:
    
    *   you have a small file <\= 256kb
    *   you don't want to upload and host the file somewhere
    *   you don't need to use the file again (Replicate will not store it)
    
    Show more
    
*   versionstringRequired
    
    The ID of the model version that you want to run.
    
*   webhookstring
    
    An HTTPS URL for receiving a webhook when the prediction has new output. The webhook will be a POST request where the request body is the same as the response body of the [get prediction](https://replicate.com/cudanexus/nougat/api/api-reference#predictions.get) operation. If there are network problems, we will retry the webhook a few times, so make sure it can be safely called more than once. Replicate will not follow redirects when sending webhook requests to your service, so be sure to specify a URL that will resolve without redirecting.
    
    Show more
    
*   webhook\_events\_filterarray
    
    By default, we will send requests to your webhook URL whenever there are new outputs or the prediction has finished. You can change which events trigger webhook requests by specifying `webhook_events_filter` in the prediction request:
    
    *   `start`: immediately on prediction start
    *   `output`: each time a prediction generates an output (note that predictions can generate multiple outputs)
    *   `logs`: each time log output is generated by a prediction
    *   `completed`: when the prediction reaches a terminal state (succeeded/canceled/failed)
    
    For example, if you only wanted requests to be sent at the start and end of the prediction, you would provide:
    
    ```json
    {
      "version": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
      "input": {
        "text": "Alice"
      },
      "webhook": "https://example.com/my-webhook",
      "webhook_events_filter": ["start", "completed"]
    }
    ```
    
    Requests for event types `output` and `logs` will be sent at most once every 500ms. If you request `start` and `completed` webhooks, then they'll always be sent regardless of throttling.
    
    Show more
    

Examples

Create

Create a prediction and get the output

Webhooks

Create a new prediction using webhooks

Make a request

post/predictions

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

Get a prediction

predictions.get

Input parameters

*   prediction\_idstringRequired
    
    The ID of the prediction to get.
    

Examples

Get

Get the latest version of a prediction by id

Make a request

get/predictions/{prediction\_id}

```javascript
import Replicate from "replicate";
const replicate = new Replicate();

console.log("Getting prediction...")
const prediction = await replicate.predictions.get(predictionId);
//=> {"id": "xyz...", "status": "successful", ... }
```

Copy

Cancel a prediction

predictions.cancel

Input parameters

*   prediction\_idstringRequired
    
    The ID of the prediction to cancel.
    

Examples

Cancel

Cancel an in progress prediction

Make a request

post/predictions/{prediction\_id}/cancel

```javascript
import Replicate from "replicate";
const replicate = new Replicate();

console.log("Canceling prediction...")
const prediction = await replicate.predictions.cancel(predictionId);
//=> {"id": "xyz...", "status": "canceled", ... }
```

Copy

List predictions

predictions.list

Examples

List

List the first page of your predictions

Paginate

Iterate through all your predictions

Make a request

get/predictions

```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const page = await replicate.predictions.list();
console.log(page.results)
//=> [{ "id": "xyz...", "status": "successful", ... }, { ... }]
```

Copy

[Replicate](https://replicate.com/)

[Home](https://replicate.com/home) [About](https://replicate.com/about) [Guides](https://replicate.com/guides) [Newsletter](https://replicate.com/newsletter) [Terms](https://replicate.com/terms) [Privacy](https://replicate.com/privacy) [Status](https://replicatestatus.com/) [GitHub](https://github.com/replicate) [X](https://x.com/replicate) [Discord](https://discord.gg/replicate) [Support](https://replicate.com/support) 

  

Copy model name

**This model is cold.** You'll get a fast response if the model is warm and already running, and a slower response if the model is cold and starting up.

System theme

Light theme

Dark theme

Copy

Copy

Copy

Copy