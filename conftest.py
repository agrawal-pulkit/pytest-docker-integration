import docker
import pytest
import subprocess
import MySQLdb

# dclient = docker.DockerClient(base_url='unix://var/run/docker.sock')
dclient = docker.from_env()

@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    print("\n====SETUP====")
    docker_compose_up()
    create_schema()
    yield

    print("\n====CLEANUP====")
    delete_schema()
    # docker_compose_down()
    for container in dclient.containers.list(filters={"label":"qe.test.containers=true"}):
        print("container", container)
        try:
            container.stop()
            container.remove()
        except Exception as e:
            print("Error: ", e)

def docker_compose_up(build=True):
    command = ['docker-compose', 'up', "-d", "--force-recreate"]
    if build:
        command.append('--build')

    subprocess.run(command, stdout=subprocess.DEVNULL)

def docker_compose_down():
    command = ['docker-compose', 'down']
    subprocess.run(command, stdout=subprocess.DEVNULL)

def db_connection():
    try:
        db_conn = MySQLdb.connect(host='0.0.0.0',user='ipa',passwd='password',db='ipa')
        cursor = db_conn.cursor()
        return db_conn,cursor
    except MySQLdb.Error as e:
        print("Exception in db connection: ", e)

def execute_query(sql):
    try:
        conn, cursor = db_connection()
        cursor.execute(sql)
        cursor.close() 
        conn.commit()
        conn.close()
    except MySQLdb.Error as e:
        print("Exception in execute query: ", e)
    
def create_schema():
    sql = """
    use ipa;
    CREATE TABLE employee ( 
        name VARCHAR(100) NOT NULL, 
        age INT NOT NULL 
    );
    """
    execute_query(sql)
    

def delete_schema():
    sql = """
    use ipa;
    DROP TABLE employee ;
    """
    execute_query(sql)


