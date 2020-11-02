def smth(num, num_2):
    if num_2 == 1:
        return num
    return num * (smth(num, num_2 - 1))

def smth_2(num, num_2): 
    x = 1
    for _ in range(num_2):
        x *= num
    return x

print(smth(2, 2))
print(smth_2(2, 2))

<div class="card mb-3" style="max-width: 540px;">
                  <div class="row no-gutters">
                    <div class="col-md-4">
                      <img src="{{ edition.cover }}" class="card-img">
                    </div>
                    <div class="col-md-8">
                      <div class="card-body">
                        {% for author in edition.my_authors %}
                          <h5 class="card-title">{{ author }}</p></h5>
                        {% endfor %}
                        <h5><a href='/book/{{ edition.id }} '>{{ edition }}</a></h5>
                        <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
                      </div>
                    </div>
                  </div>
                </div></a>

                <form action='/search/' method="GET" class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" name='q' type="search" placeholder="Искать" aria-label="Search">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Искать</button>
      </form>