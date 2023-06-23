# demo_docker

A small repo to show how to dockerize your ML model.

---
## How to use the repo

- Create processed data from raw data:

```bash
python src/data/make_dataset.py -i data/raw/iris.csv -o data/processed/iris_processed.csv
```

- Create feature engineered data from processed data:

```bash
python src/features/build_features.py -i data/processed/iris_processed.csv -o data/processed/iris_features.csv
```

- Train the model:

```bash
python src/models/train_model.py -i data/processed/iris_features.csv -o models/iris_model.pkl
```

- Run inference app:

```bash
bash run_app.sh
```

---
## Using docker

- Build the image:

```bash
docker build -t demo_image .
```

- Run the container:

```bash
docker run --name demo_container -it -d -p 8080:8080 demo_image
```