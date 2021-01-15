from models import prepare_save


def test_prepare_save():
	error = 'Unrightable behavior`s from function prepare_save'
	
	assert prepare_save('  @@#21fskdlf; !33d  ') == '21fskdlf 33d', error
	assert prepare_save(' fff  ') == 'fff', error
	assert prepare_save('\ngfdgd\nfd\n') == 'gfdgdfd', error
	assert prepare_save('FFFF') == 'ffff', error


if __name__ == '__main__':
	test_prepare_save()