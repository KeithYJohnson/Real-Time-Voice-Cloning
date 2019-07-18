# build command:
# >> docker build -t voice-base .
#
# run command:
# >> docker run -it --rm --init --runtime=nvidia --ipc=host --volume="$PWD:/workspace" -e NVIDIA_VISIBLE_DEVICES=0 -p 80:80  voice-base

FROM pytorch/pytorch

WORKDIR "/workspace"
RUN apt-get clean \
        && apt-get update \
        && apt-get install -y ffmpeg libportaudio2 openssh-server python3-pyqt5 xauth \
        && apt-get -y autoremove \
        && mkdir /var/run/sshd \
        && mkdir /root/.ssh \
        && chmod 700 /root/.ssh \
        && ssh-keygen -A \
        && sed -i "s/^.*PasswordAuthentication.*$/PasswordAuthentication no/" /etc/ssh/sshd_config \
        && sed -i "s/^.*X11Forwarding.*$/X11Forwarding yes/" /etc/ssh/sshd_config \
        && sed -i "s/^.*X11UseLocalhost.*$/X11UseLocalhost no/" /etc/ssh/sshd_config \
        && grep "^X11UseLocalhost" /etc/ssh/sshd_config || echo "X11UseLocalhost no" >> /etc/ssh/sshd_config
ADD Real-Time-Voice-Cloning/requirements.txt /workspace/requirements.txt
RUN pip install -r /workspace/requirements.txt
RUN echo "export PATH=/opt/conda/bin:$PATH" >> /root/.profile
RUN pip install flask --user
ENTRYPOINT ["sh", "-c", "/usr/sbin/sshd && bash"]
CMD ["bash"]