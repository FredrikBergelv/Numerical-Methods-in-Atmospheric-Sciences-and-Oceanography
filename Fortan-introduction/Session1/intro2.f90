program lec_01
    implicit none

    ! Declaration of variables
    INTEGER :: iindex

    ! Initialization
    iindex = 2

    ! If block
    if(iindex > 0) then
        print *, 'POSITIVE', iindex
    elseif (iindex < 0) then
        print *, 'NEGATIVE', iindex
    else 
        print *, 'THE NUMBER IS ZERO', 0
    end if 

end program lec_01
