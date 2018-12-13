FROM python:3.6

#RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list && \
#    curl https://bazel.build/bazel-release.pub.gpg | apt-key add - && \
#    apt update && apt install -y bazel && apt clean
#
#RUN apt update && apt install -y python-numpy && apt clean
#RUN cd /tmp && git clone --depth 1 https://github.com/tensorflow/tensorflow.git -b r1.12
#RUN cd /tmp/tensorflow && git submodule update && \
#    ./configure && \
#    bazel build --action_env PYTHON_BIN_PATH=/usr/bin/python --incompatible_remove_native_http_archive=false -c opt --copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-mfpmath=both --copt=-msse4.2 -k //tensorflow/tools/pip_package:build_pip_package && \
#    ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
#RUN pip install /tmp/tensorflow_pkg/tensorflow-1.12.whl

COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --upgrade -r /tmp/requirements.txt

WORKDIR /app

ENTRYPOINT ["./run.py"]

VOLUME /app
