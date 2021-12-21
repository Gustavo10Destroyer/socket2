import threading

class Listener:
  def __init__(self, type, event, callback):
    self._type = type
    self._event = event
    self.__callback = callback
    
    self._is_destroyed = False
  
  def destroy_listener(self, listeners) -> bool:
    if type(listeners) == Listeners:
      if not self._is_destroyed:
        if self._event in listeners[self._type]:
          if self.__callback in listeners[self._type][self._event]:
            listeners[self._type][self._event].remove(self.__callback)
            
            self._is_destroyed = True
            return True
          else:
            self._is_destroyed = True
            return True
        else:
          return False
      else:
        raise Exception("Este ouvinte já foi destruído!")
    else:
      raise TypeError("'listeners' precisa ser uma instância Listeners!")

class Listeners:
  def __init__(self):
    self.on = {}
    self.once = {}
  
  def __getitem__(self, key):
    if key == "on":
      return self.on
    elif key == "once":
      return self.once
    else:
      raise Exception("Valor inválido!")

class EmitterSync:
  def __init__(self):
    self._listeners = Listeners()
  
  def on(self, callback):
    event = callback.__name__
    
    if not event in self._listeners.on:
      self._listeners.on[event] = []
    
    self._listeners.on[event].append(callback)
    
    return Listener("on", event, callback)
  
  def once(self, callback):
    event = callback.__name__
    
    if not event in self._listeners.once:
      self._listeners.once[event] = []
    
    self._listeners.once[event].append(callback)
    
    return Listener("once", event, callback)

  def emit(self, event, *args):
    if event in self._listeners.on:
      for callback in self._listeners.on[event]:
        callback(*args)

    if event in self._listeners.once:
      for callback in self._listeners.once[event]:
        callback(*args)

        self._listeners.once[event].remove(callback)

  def remove_listener(self, listener):
    listener.destroy_listener(self._listeners)

class EmitterAsync:
  def __init__(self):
    self._listeners = Listeners()
  
  def on(self, callback):
    event = callback.__name__
    
    if not event in self._listeners.on:
      self._listeners.on[event] = []
    
    self._listeners.on[event].append(callback)
  
    return Listener("on", event, callback)
  
  def once(self, callback):
    event = callback.__name__
    
    if not event in self._listeners.once:
      self._listeners.once[event] = []
    
    self._listeners.once[event].append(callback)

    return Listener("once", event, callback)

  def emit(self, event, *args):
    if event in self._listeners.on:
      for callback in self._listeners.on[event]:
        threading.Thread(target=callback, args=args).start()

    if event in self._listeners.once:
      for callback in self._listeners.once[event]:
        threading.Thread(target=callback, args=args).start()

        self._listeners.once[event].remove(callback)
  
  def remove_listener(self, listener):
    listener.destroy_listener(self._listeners)