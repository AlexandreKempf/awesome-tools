import torch.optim as optim
import torch.optim.lr_scheduler as sched
import torch.nn as nn


def optimizer(model, type, scheduler=None, lr=None, decay=0, time=30):
    """
    time is the temporal parameter for the scheduler
    """
    if lr is None:
        kwargs_opti = {}
    else:
        kwargs_opti = {'lr': lr}

    # OPTIMIZER
    if type == 'SGD':
        kwargs_opti['momentum'] = 0.9
        optimizer = optim.SGD(model.parameters(), **kwargs_opti)

    elif type == 'Adam':
        optimizer = optim.Adam(model.parameters(), **kwargs_opti)

    elif type == 'RMSprop':
        optimizer = optim.RMSprop(model.parameters(), **kwargs_opti)

    # SCHEDULER
    kwargs_sched = {}
    if scheduler is None:  # no change in learning_rate
        kwargs_sched['step_size'] = 1
        kwargs_sched['gamma'] = 0
        scheduler = sched.StepLR(optimizer, **kwargs_sched)

    elif scheduler == 'StepLR':
        kwargs_sched['step_size'] = time
        kwargs_sched['gamma'] = decay
        scheduler = sched.StepLR(optimizer, **kwargs_sched)

    elif scheduler == 'MultiStepLR':
        kwargs_sched['milestones'] = time
        kwargs_sched['gamma'] = decay
        scheduler = sched.MultiStepLR(optimizer, **kwargs_sched)

    elif scheduler == 'CosineAnnealingLR':
        kwargs_sched['T_max'] = time
        scheduler = sched.CosineAnnealingLR(optimizer, **kwargs_sched)

    elif scheduler == 'ReduceLROnPlateau':
        kwargs_sched['patience'] = time
        kwargs_sched['factor'] = decay
        scheduler = sched.ReduceLROnPlateau(optimizer, **kwargs_sched)

    return (optimizer, scheduler)



def train_DL(model, data, criterion, optimizer, epoch):

    (optimizer, scheduler) = optimizer

    if criterion == 'cross_entropy':
        criterion = nn.CrossEntropyLoss()

    for ep in range(epoch):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, d in enumerate(data, 0):
            # get the inputs; d is a list of [inputs, labels]
            inputs, labels = d

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()

            # print statistics
            running_loss += loss.item()
            if i % 20 == 0:    # print every 20 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (ep + 1, i + 1, running_loss / 20))
                running_loss = 0.0
            print('Finished Training')
    return model




# RUN MODEL
# PICK BEST
# SAVE MODEL
# LOAD MODEL

# CREATE DATACONTAINER FROM BATCH OR LIST
# SAVE DATACONTAINER
# LOAD DATACONTAINER
