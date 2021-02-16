# pdf-gen
A service for converting HTML to a PDF buffer

<img src="https://user-images.githubusercontent.com/42006114/97615019-2005dd00-19f1-11eb-8e5b-3b37aa393163.jpeg" />

## Endpoints

#### `convert/`
##### request:
```http request
POST /api/v1/convert/
```
body:
```json
{
  "data": "HTML to convert to PDF"
}
```

##### response:
```
Content-Type: application/pdf
```
This enpoint simply takes in HTML from the `data` property of the body and returns a PDF buffer. Put any CSS inside a `<style>` tag in the `<head>`.

---

#### `convert-with-metadata/`
##### request:
```http request
POST /api/v1/convert-with-metadata/
```
body:
```json
{
  "data": "HTML to convert to PDF"
}
```

##### response:
example:
```json
{
  "id": 12
}
```
This endpoint takes in the same HTML string as `convert/`, but instead returns a JSON object with a unique `id` property. You can then use that id in the following endpoints to retrieve the anchor locations and stored PDF.

---

#### `metadata/<id>/`
##### request:
```http request
GET /api/v1/metadata/<id>/
```

##### response:
example:
```json
[
  {
    "example_anchor1": [
      [
        579.046875,
        208.38
      ]
    ],
    "example_anchor2": [
      [
        427.354,
        305.21879
      ],
      [
        430.5,
        106.25
      ]
    ]
  },
  {
    "example_anchor3": [
      [
        123.4,
        654.321
      ]
    ]
  }
]
```
Given an id from `convert-with-metadata/`, this endpoint will return a JSON list of all pages in the associated PDF, each with a list of anchors and their x/y coordinates on that page.

The data is structured as an array of pages, each represented as an object. Each page object will have properties with the names of each anchor on that page, and each anchor will have a 2D array of x/y coordinates, represented as floats.

---

#### `doc/<id>/`
##### request:
```http request
GET /api/v1/doc/<id>/
```

##### response:
```
Content-Type: application/pdf
```
Given an id from `convert-with-metadata/`, this endpoint will return a PDF buffer of the converted HTML, just like `convert/`.
