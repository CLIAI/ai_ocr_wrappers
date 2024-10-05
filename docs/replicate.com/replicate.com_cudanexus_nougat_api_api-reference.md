Here's a nicely organized Markdown file showing the API for different languages:

# cudanexus/nougat API Reference

## Table of Contents
- [Create a Prediction](#create-a-prediction)
- [Get a Prediction](#get-a-prediction)
- [Cancel a Prediction](#cancel-a-prediction)
- [List Predictions](#list-predictions)

## Create a Prediction

### Endpoint
```
POST /predictions
```

### Request Body Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| input | object | Yes | The model's input as a JSON object |
| version | string | Yes | The ID of the model version to run |
| webhook | string | No | An HTTPS URL for receiving a webhook |
| webhook_events_filter | array | No | Specify which events trigger webhook requests |

### Example (JavaScript)
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const input = {
    pdf_file: "https://replicate.delivery/pbxt/KADiqRc7gGx6AaacKyClxzVoIg24BchawSogWsQvKvzoGED5/calculus00marciala_0136.pdf"
};

const output = await replicate.run("cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76", { input });
console.log(output);
```

## Get a Prediction

### Endpoint
```
GET /predictions/{prediction_id}
```

### Input Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prediction_id | string | Yes | The ID of the prediction to get |

### Example (JavaScript)
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

console.log("Getting prediction...");
const prediction = await replicate.predictions.get(predictionId);
```

## Cancel a Prediction

### Endpoint
```
POST /predictions/{prediction_id}/cancel
```

### Input Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prediction_id | string | Yes | The ID of the prediction to cancel |

### Example (JavaScript)
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

console.log("Canceling prediction...");
const prediction = await replicate.predictions.cancel(predictionId);
```

## List Predictions

### Endpoint
```
GET /predictions
```

### Example (JavaScript)
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const page = await replicate.predictions.list();
console.log(page.results);
```

---

For more information and examples in other languages, please refer to the [official API documentation](https://replicate.com/cudanexus/nougat/api/api-reference).

