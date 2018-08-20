### Here we need to state the requirement for the platform:

Python
Java
HTML
Parsers
Django

## Installing

### Setup Virtualenv and install requirements

Install Virtualenv

```
pip install virtualenv
```


Setup up Virtualenv in project

```
virtualenv venv
source venv/bin/activate
```

Install packages

```
pip install -r requirements.txt
```

```
cd front; yarn
```


## Running

- Run everything together

  ```
  ./venv/bin/honcho start
  ```

- Or separately:

    - Django server

    ```
    source venv/bin/activate; python manage.py runserver
    ```

    - Webpack dev server

    ```
    cd front; yarn start
    ```


## React

### Rendering components from Django views

1. Pass props to the view as a JSON encoded dict:

  ```python
  locals = {
      'props' : json.dumps({
          'title': exercise_title,
          'text': self.prob_cons.prob_in.text,
          'totalSteps': self.num_steps
      })
  }
  ```

1. Render the HTML element

  ```html
  <div data-react-component="Problem" data-react-props="{{props}}"></div>
  ```

1. Import the file in `index.js` and add an entry to the `components` map:

  ```javascript
  import Problem from "./Problem";
  ...
  const components = {
    ...
    'Problem': Problem,
  };
  ```

## Code Quality

### ESLint

Analyzes JS looking for problematic patterns.

```
yarn eslint
```

### Prettier

Formats JS code.

```
yarn prettier
```
