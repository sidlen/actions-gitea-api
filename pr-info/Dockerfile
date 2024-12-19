FROM git.softline.com/registry/python-image:v4
COPY pr.py /pr.py
ENTRYPOINT ["sh", "-c", "python /pr.py && echo \"::set-output name=output_data::$(cat output.json)\""]